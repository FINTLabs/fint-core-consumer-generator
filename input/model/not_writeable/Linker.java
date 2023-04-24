package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCES;
import no.fint.relations.FintLinker;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

import java.util.Collection;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import static java.util.Objects.isNull;

@Component
public class MODELLinker extends FintLinker<MODEL_RESOURCE> {

    public MODELLinker() {
        super(MODEL_RESOURCE.class);
    }

    public void mapLinks(MODEL_RESOURCE resource) {
        super.mapLinks(resource);
    }

    @Override
    public MODEL_RESOURCES toResources(Collection<MODEL_RESOURCE> collection) {
        return toResources(collection.stream(), 0, 0, collection.size());
    }

    @Override
    public MODEL_RESOURCES toResources(Stream<MODEL_RESOURCE> stream, int offset, int size, int totalItems) {
        MODEL_RESOURCES resources = new MODEL_RESOURCES();
        stream.map(this::toResource).forEach(resources::addResource);
        addPagination(resources, offset, size, totalItems);
        return resources;
    }

    @Override
    public String getSelfHref(MODEL_RESOURCE MODEL_LOWER) {
        return getAllSelfHrefs(MODEL_LOWER).findFirst().orElse(null);
    }


    @Override
    public Stream<String> getAllSelfHrefs(MODEL_RESOURCE MODEL_LOWER) {
        Stream.Builder<String> builder = Stream.builder();
        if (!isNull(MODEL_LOWER.getSystemId()) && !StringUtils.isEmpty(MODEL_LOWER.getSystemId().getIdentifikatorverdi())) {
            builder.add(createHrefWithId(MODEL_LOWER.getSystemId().getIdentifikatorverdi(), "systemid"));
        }

        return builder.build();
    }

    int[] hashCodes(MODEL_RESOURCE MODEL_LOWER) {
        IntStream.Builder builder = IntStream.builder();
        if (!isNull(MODEL_LOWER.getSystemId()) && !StringUtils.isEmpty(MODEL_LOWER.getSystemId().getIdentifikatorverdi())) {
            builder.add(MODEL_LOWER.getSystemId().getIdentifikatorverdi().hashCode());
        }

        return builder.build().toArray();
    }
}