package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.core.consumer.shared.resource.event.EventResponseKafkaConsumer;
import no.fintlabs.kafka.event.EventConsumerFactoryService;
import org.springframework.stereotype.Service;

@Service
public class MODELResponseKafkaConsumer extends EventResponseKafkaConsumer<MODEL_RESOURCE> {

    public MODELResponseKafkaConsumer(EventConsumerFactoryService eventConsumerFactoryService, MODELConfig MODEL_LOWERConfig, MODELLinker MODEL_LOWERLinker) {
        super(eventConsumerFactoryService, MODEL_LOWERConfig, MODEL_LOWERLinker);
    }

}
