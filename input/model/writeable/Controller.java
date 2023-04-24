package no.fintlabs.consumer.model.MODEL_LOWER;

import lombok.extern.slf4j.Slf4j;
import no.fint.antlr.FintFilterService;
import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fint.relations.FintRelationsMediaType;
import no.fintlabs.consumer.config.RestEndpoints;
import no.fintlabs.core.consumer.shared.resource.CacheService;
import no.fintlabs.core.consumer.shared.resource.WriteableConsumerRestController;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@CrossOrigin
@RestController
@RequestMapping(name = "MODEL", value = RestEndpoints.MODEL_UPPER, produces = {FintRelationsMediaType.APPLICATION_HAL_JSON_VALUE, MediaType.APPLICATION_JSON_VALUE})
public class MODELController extends WriteableConsumerRestController<MODEL_RESOURCE> {

    public MODELController(
            CacheService<MODEL_RESOURCE> cacheService,
            MODELLinker fintLinker,
            MODELConfig MODEL_LOWERConfig,
            MODELEventKafkaProducer MODEL_LOWEREventKafkaProducer,
            MODELResponseKafkaConsumer MODEL_LOWERResponseKafkaConsumer,
            FintFilterService odataFilterService,
            MODELRequestKafkaConsumer MODEL_LOWERRequestKafkaConsumer) {
        super(cacheService, fintLinker, MODEL_LOWERConfig, MODEL_LOWEREventKafkaProducer, MODEL_LOWERResponseKafkaConsumer, odataFilterService, MODEL_LOWERRequestKafkaConsumer);
    }
}
